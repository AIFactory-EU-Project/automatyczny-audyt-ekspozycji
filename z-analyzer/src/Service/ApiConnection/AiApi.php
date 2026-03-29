<?php

namespace App\Service\ApiConnection;

use App\Entity\Camera;
use App\Entity\File;
use App\Entity\Photo;
use App\Entity\Planogram;
use App\Exception\AiPhotoProcessException;
use App\Exception\ApiClientException;
use App\Exception\FileAccessException;
use App\Exception\PhotoWithoutLinkedFileException;
use App\Provider\ApiClient;
use App\Service\StorageRetriever;
use App\Service\TmpImageFileHandler;
use App\Service\Uploader\LocalStorage;
use App\Utility\DataObject\GrillReport;
use App\Utility\DataObject\PlanogramReport;
use App\Utility\DBAL\Type\FileStorageType;
use App\Utility\DBAL\Type\SegmentType;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Component\DependencyInjection\ParameterBag\ParameterBagInterface;
use Symfony\Component\Mime\Part\DataPart;
use Symfony\Component\Mime\Part\Multipart\FormDataPart;

class AiApi
{
    private ApiClient $client;
    private EntityManagerInterface $entityManager;
    private ParameterBagInterface $params;
    private TmpImageFileHandler $tmpImageFileHandler;
    private LocalStorage $fileStorage;
    private StorageRetriever $storageRetriever;
    private string $aiServiceAddress;

    public function __construct(
        ApiClient $client,
        EntityManagerInterface $entityManager,
        ParameterBagInterface $params,
        TmpImageFileHandler $tmpImageFileHandler,
        LocalStorage $fileStorage,
        StorageRetriever $storageRetriever
    ) {
        $this->client = $client;
        $this->entityManager = $entityManager;
        $this->params = $params;
        $this->tmpImageFileHandler = $tmpImageFileHandler;
        $this->fileStorage = $fileStorage;
        $this->storageRetriever = $storageRetriever;
        $this->aiServiceAddress = $params->get('ecosystem')['ai_service']['location'];
    }

    /**
     * @param Photo $photo
     * @return bool
     * @throws AiPhotoProcessException
     */
    public function verifyPhoto(Photo $photo): bool
    {
        $segmentType = $photo->getCamera()
            ->getSegment()
            ->getType();
        switch ($segmentType) {
            case SegmentType::READY_MEAL:
            case SegmentType::QUICK_SNACK:
                $fullAddr = $this->aiServiceAddress . '/verify-shelf-photo-valid-for-analysis';
                break;
            case SegmentType::GRILL:
                $fullAddr = $this->aiServiceAddress . '/verify-grill-photo-valid-for-analysis';
                break;
            default:
                return false;
        }

        try {
            $file = $this->storageRetriever->getFileFromPhoto($photo);
        } catch (PhotoWithoutLinkedFileException $e) {
            throw new AiPhotoProcessException($e->getMessage());
        }

        try {
            $formFields = [
                'image' => DataPart::fromPath($file->getFullPath()),
            ];
            $formData = new FormDataPart($formFields);
            $this->client->request(
                $fullAddr,
                ApiClient::METHOD_POST,
                $formData->bodyToIterable(),
                $formData->getPreparedHeaders()->toArray()
            );
        } catch (ApiClientException $e) {
            throw new AiPhotoProcessException($e->getMessage());
        }

        return true;
    }

    /**
     * @param Photo $photo
     * @return Photo
     * @throws AiPhotoProcessException
     */
    public function removeFaces(Photo $photo): Photo
    {
        try {
            $file = $this->storageRetriever->getFileFromPhoto($photo);
        } catch (PhotoWithoutLinkedFileException $e) {
            throw new AiPhotoProcessException($e->getMessage());
        }

        $fullAddr = $this->aiServiceAddress . '/remove-faces-from-photo';

        try {
            $formFields = [
                'image' => DataPart::fromPath($file->getFullPath()),
            ];
            $formData = new FormDataPart($formFields);
            $content = $this->client->request(
                $fullAddr,
                ApiClient::METHOD_POST,
                $formData->bodyToIterable(),
                $formData->getPreparedHeaders()->toArray()
            );
        } catch (ApiClientException $e) {
            throw new AiPhotoProcessException($e->getMessage());
        }

        try {
            $tmpFileObject = $this->tmpImageFileHandler->saveTmpPngFromStream($content);
        } catch (FileAccessException $e) {
            throw new AiPhotoProcessException($e->getMessage());
        }

        $file = $this->fileStorage->uploadFile($tmpFileObject, false);

        return $this->createFacelessPhotoEntity($photo->getCamera(), $file);
    }

    /**
     * @param Photo $photo
     * @return GrillReport
     * @throws AiPhotoProcessException
     */
    public function getGrillReport(Photo $photo): GrillReport
    {
        $fullAddr = $this->aiServiceAddress . '/generate-grill-report';

        try {
            $file = $this->storageRetriever->getFileFromPhoto($photo);
        } catch (PhotoWithoutLinkedFileException $e) {
            throw new AiPhotoProcessException($e->getMessage());
        }

        try {
            $formFields = [
                'image' => DataPart::fromPath($file->getFullPath()),
            ];
            $formData = new FormDataPart($formFields);
            $content = $this->client->request(
                $fullAddr,
                ApiClient::METHOD_POST,
                $formData->bodyToIterable(),
                $formData->getPreparedHeaders()->toArray()
            );
        } catch (ApiClientException $e) {
            throw new AiPhotoProcessException($e->getMessage());
        }

        return $this->createGrillReport(json_decode($content, true));
    }

    /**
     * @param Photo $photo
     * @param Planogram $planogram
     * @param Camera $camera
     * @return PlanogramReport
     * @throws AiPhotoProcessException
     */
    public function getPlanogramReport(Photo $photo, Planogram $planogram, Camera $camera): PlanogramReport
    {
        $fullAddr = $this->aiServiceAddress . '/generate-planogram-report';

        try {
            $file = $this->storageRetriever->getFileFromPhoto($photo);
        } catch (PhotoWithoutLinkedFileException $e) {
            throw new AiPhotoProcessException($e->getMessage());
        }

        try {
            $formFields = [
                'image' => DataPart::fromPath($file->getFullPath()),
                'planogramId' => (string) $planogram->getNeuralNetworkId(),
                'cameraIp' => $camera->getIp(),
            ];
            $formData = new FormDataPart($formFields);
            $content = $this->client->request(
                $fullAddr,
                ApiClient::METHOD_POST,
                $formData->bodyToIterable(),
                $formData->getPreparedHeaders()->toArray()
            );
        } catch (ApiClientException $e) {
            throw new AiPhotoProcessException($e->getMessage());
        }

        return $this->createPlanogramReport(json_decode($content, true));
    }

    /**
     * @param Camera $camera
     * @param File $file
     * @return Photo
     */
    private function createFacelessPhotoEntity(Camera $camera, File $file)
    {
        $photoEntity = new Photo();
        $photoEntity
            ->setCamera($camera)
            ->setIsAiProcessed(false)
            ->setIsManipulated(true)
            ->setIsValid(true)
            ->setStorageId((string) $file->getId())
            ->setStorageType(FileStorageType::LOCAL);

        $this->entityManager->persist($photoEntity);
        $this->entityManager->flush();

        return $photoEntity;
    }

    /**
     * @param array $data
     * @return GrillReport
     */
    private function createGrillReport(array $data): GrillReport
    {
        $report = new GrillReport;
        $report->count = $data['result']['count'];
        return $report;
    }

    /**
     * @param array $data
     * @return PlanogramReport
     */
    private function createPlanogramReport(array $data): PlanogramReport
    {
        $report = new PlanogramReport();
        $report->boxes = $data['result']['boxes'];
        return $report;
    }
}
