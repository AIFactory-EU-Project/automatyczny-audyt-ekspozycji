<?php

namespace App\Service;

use App\Entity\Camera;
use App\Entity\FailedImportAttempt;
use App\Entity\Photo;
use App\Entity\Planogram;
use App\Entity\ReportPhotoAnalysis;
use App\Entity\ShopPlanogramAssignment;
use App\Exception\AiPhotoProcessException;
use App\Exception\CameraCaptureException;
use App\Exception\ImageManipulationException;
use App\Exception\PhotoWithoutLinkedFileException;
use App\Service\ApiConnection\AiApi;
use App\Service\ApiConnection\CameraApi;
use App\Service\Uploader\LocalStorage;
use App\Utility\DBAL\Type\SegmentType;
use Doctrine\Common\Collections\Collection;
use Doctrine\ORM\EntityManagerInterface;
use Psr\Log\LoggerInterface;
use Symfony\Component\DependencyInjection\ContainerInterface;
use Exception;
use Symfony\Component\HttpFoundation\File\File;

class ImportProcessHandler
{
    private ContainerInterface $container;
    private CameraApi $cameraApi;
    private AiApi $aiApi;
    private ImageManipulator $imageManipulator;
    private EntityManagerInterface $em;
    private LoggerInterface $logger;
    private StorageRetriever $storageRetriever;
    private LocalStorage $fileStorage;

    public function __construct(
        ContainerInterface $container,
        CameraApi $cameraApi,
        AiApi $aiApi,
        ImageManipulator $imageManipulator,
        EntityManagerInterface $em,
        LoggerInterface $logger,
        StorageRetriever $storageRetriever,
        LocalStorage $localStorage
    ) {
        $this->container = $container;
        $this->cameraApi = $cameraApi;
        $this->aiApi = $aiApi;
        $this->imageManipulator = $imageManipulator;
        $this->em = $em;
        $this->logger = $logger;
        $this->storageRetriever = $storageRetriever;
        $this->fileStorage = $localStorage;
    }

    /**
     * @param Collection $collection
     */
    public function importFromCameras(Collection $collection)
    {
        if ($collection->count() === 0) {
            return;
        }

        $cameras = $collection->getValues();
        // TODO optimize by opening db session and setting entity relation depths
        /** @var Camera $camera */
        foreach ($cameras as $camera) {
            try {
                $currPhoto = $this->cameraApi->getPhoto($camera);
            } catch (CameraCaptureException $e) {
                $this->createFailedImportAttempt($camera, $e);
                continue;
            }

            try {
                $rotatedPhoto = $this->imageManipulator->rotateWithSettings($currPhoto);
            } catch (ImageManipulationException $e) {
                $this->createFailedImportAttempt($camera, $e);
                continue;
            }

            try {
                $this->aiApi->verifyPhoto($rotatedPhoto);
            } catch (AiPhotoProcessException $e) {
                $this->createFailedImportAttempt($camera, $e);
                continue;
            }

            try {
                $photoWithoutFaces = $this->aiApi->removeFaces($rotatedPhoto);
            } catch (AiPhotoProcessException $e) {
                $this->createFailedImportAttempt($camera, $e);
                continue;
            }

            try {
                $manipulatedPhoto = $this->imageManipulator->transformPhoto($photoWithoutFaces);
            } catch (ImageManipulationException $e) {
                $this->createFailedImportAttempt($camera, $e);
                continue;
            }

            $reportAnalysisEntity = new ReportPhotoAnalysis();

            try {
                switch ($camera->getSegment()->getType()) {
                    case SegmentType::QUICK_SNACK:
                    case SegmentType::READY_MEAL:
                        $planogram = $this->getPlanogramByCamera($camera);
                        $report = $this->aiApi->getPlanogramReport($manipulatedPhoto, $planogram, $camera);
                        $reportAnalysisEntity->setPlanogram($planogram);
                        break;
                    case SegmentType::GRILL:
                        $report = $this->aiApi->getGrillReport($manipulatedPhoto);
                        break;
                    default:
                        throw new Exception('Segment not set');
                }
            } catch (AiPhotoProcessException | Exception $e) {
                $this->createFailedImportAttempt($camera, $e);
                continue;
            }

            $manipulatedPhoto->setIsAiProcessed(true);

            $reportAnalysisEntity->setData($report);
            $reportAnalysisEntity->setPhoto($manipulatedPhoto);
            $reportAnalysisEntity->setRealPhoto($photoWithoutFaces);
            $this->em->persist($reportAnalysisEntity);
            $this->em->flush();
        }
    }

    /**
     * @param Camera $camera
     * @param string $message
     */
    private function createFailedImportAttempt(Camera $camera, string $message): void
    {
        $this->logger->error($message);

        $attempt = new FailedImportAttempt();
        $attempt
            ->setCamera($camera)
            ->setReason($message)
        ;

        $doctrine = $this->container->get('doctrine');
        $manager = $doctrine->getManager();
        $manager->persist($attempt);
        $manager->flush();
    }


    /**
     * @param Camera $camera
     * @return Planogram
     * @throws Exception
     */
    private function getPlanogramByCamera(Camera $camera): Planogram
    {
        $planogramAssignmentRepository = $this
            ->em
            ->getRepository(ShopPlanogramAssignment::class)
        ;

        /** @var ShopPlanogramAssignment $planogramAssignment */
        $planogramAssignment = $planogramAssignmentRepository->getCurrentPlanogramAssignmentByShopAndSegment(
            $camera->getShop(),
            $camera->getSegment()
        );

        if (!$planogramAssignment) {
            throw new Exception(
                'Planogram assigment for shop ' .
                $camera->getShop()->getId() .
                ' and segment: ' .
                $camera->getSegment()->getType() .
                ' not found. Camera id: ' . $camera->getId()
            );
        }

        return $planogramAssignment->getPlanogram();
    }
}
