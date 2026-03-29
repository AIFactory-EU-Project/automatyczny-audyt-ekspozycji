<?php

namespace App\Service\ApiConnection;

use App\Entity\Camera;
use App\Entity\Photo;
use App\Exception\ApiClientException;
use App\Exception\CameraCaptureException;
use App\Exception\FileAccessException;
use App\Provider\ApiClient;
use App\Service\TmpImageFileHandler;
use App\Service\Uploader\LocalStorage;
use App\Utility\DBAL\Type\FileStorageType;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Component\DependencyInjection\ParameterBag\ParameterBagInterface;

class CameraApi
{
    private ApiClient $client;
    private EntityManagerInterface $entityManager;
    private ParameterBagInterface $params;
    private TmpImageFileHandler $tmpImageFileHandler;
    private LocalStorage $fileStorage;

    public function __construct(
        ApiClient $client,
        EntityManagerInterface $entityManager,
        ParameterBagInterface $params,
        TmpImageFileHandler $tmpImageFileHandler,
        LocalStorage $fileStorage
    ) {
        $this->client = $client;
        $this->entityManager = $entityManager;
        $this->params = $params;
        $this->tmpImageFileHandler = $tmpImageFileHandler;
        $this->fileStorage = $fileStorage;
    }

    /**
     * @param Camera $camera
     * @return Photo
     * @throws CameraCaptureException
     */
    public function getPhoto(Camera $camera): Photo
    {
        $cameraServiceAddr = $this->params->get('ecosystem')['camera_service']['location'];
        $fullAddr = $cameraServiceAddr . '/image/' . $camera->getIp() . '/' . $camera->getType();

        try {
            $content = $this->client->request(
                $fullAddr,
                ApiClient::METHOD_GET,
                null,
                null,
                [
                    'login' => $this->params->get('ecosystem')['camera_service']['credentials']['login'],
                    'password' => $this->params->get('ecosystem')['camera_service']['credentials']['password'],
                ]
            );
        } catch (ApiClientException $e) {
            throw new CameraCaptureException($e->getMessage());
        }

        try {
            $tmpFileObject = $this->tmpImageFileHandler->saveTmpPngFromStream($content);
        } catch (FileAccessException $e) {
            throw new CameraCaptureException($e->getMessage());
        }

        $file = $this->fileStorage->uploadFile($tmpFileObject, false);

        $photoEntity = new Photo();
        $photoEntity
            ->setCamera($camera)
            ->setIsAiProcessed(false)
            ->setIsManipulated(false)
            ->setIsValid(true)
            ->setStorageId((string) $file->getId())
            ->setStorageType(FileStorageType::LOCAL);

        $this->entityManager->persist($photoEntity);
        $this->entityManager->flush();

        return $photoEntity;
    }
}
