<?php

namespace App\Service;

use App\Entity\Camera;
use App\Entity\File;
use App\Entity\Photo;
use App\Exception\ImageManipulationException;
use App\Exception\ImageResourceException;
use App\Exception\PhotoWithoutLinkedFileException;
use App\Provider\ImageProcessorProvider;
use App\Service\Uploader\LocalStorage;
use App\Utility\DBAL\Type\FileStorageType;
use App\Utility\DBAL\Type\SegmentType;
use Doctrine\ORM\EntityManagerInterface;
use Exception;
use Symfony\Component\HttpFoundation\File\Exception\FileNotFoundException;
use Symfony\Component\HttpFoundation\File\File as FileObject;

class ImageManipulator
{
    private EntityManagerInterface $entityManager;
    private TmpImageFileHandler $tmpImageFileHandler;
    private LocalStorage $localStorage;
    private ImageProcessorProvider $imageProcessor;
    private StorageRetriever $storageRetriever;

    public function __construct(
        EntityManagerInterface $entityManager,
        TmpImageFileHandler $tmpImageFileHandler,
        LocalStorage $localStorage,
        ImageProcessorProvider $imageProcessor,
        StorageRetriever $storageRetriever
    ) {
        $this->entityManager = $entityManager;
        $this->tmpImageFileHandler = $tmpImageFileHandler;
        $this->localStorage = $localStorage;
        $this->imageProcessor = $imageProcessor;
        $this->storageRetriever = $storageRetriever;
    }

    /**
     * Transforms photo based on its camera parameters
     *
     * @param Photo $photo
     * @return Photo
     * @throws ImageManipulationException
     */
    public function transformPhoto(Photo $photo): Photo
    {
        try {
            $file = $this->storageRetriever->getFileFromPhoto($photo);
        } catch (PhotoWithoutLinkedFileException $e) {
            throw new ImageManipulationException();
        }

        try {
            $fileObject = new FileObject($file->getFullPath());
        } catch (FileNotFoundException $e) {
            // TODO update photo entity with invalidity?
            throw new ImageManipulationException();
        }

        // TODO switch for different image types?
        $image = $this->imageProcessor->createFromPng($fileObject->getRealPath());
        $settings = $photo->getCamera()->getManipulationSettings();

        $camera = $photo->getCamera();
        switch ($camera->getSegment()->getType()) {
            case SegmentType::QUICK_SNACK;
            case SegmentType::READY_MEAL:
                try {
                    $image = $this->imageProcessor->adjustDepth($image, $photo);
                } catch (Exception $e) {
                    throw new ImageManipulationException($e->getMessage());
                }
                if (!$image) {
                    throw new ImageManipulationException();
                }
                break;
            default:
                break;
        }

        $isCropped = $settings->cropHeight || $settings->cropWidth || $settings->cropX || $settings->cropY;
        if ($isCropped) {
            $image = $this->imageProcessor->imageCrop(
                $image,
                [
                    'x' => $settings->cropX,
                    'y' => $settings->cropY,
                    'width' => $settings->cropWidth,
                    'height' => $settings->cropHeight
                ]
            );
            if (!$image) {
                throw new ImageManipulationException();
            }
        }

        try {
            $tmpProcessedImageFile = $this->tmpImageFileHandler->saveTmpPngFromGd($image);
        } catch (ImageResourceException $e) {
            throw new ImageManipulationException();
        }
        $processedImage = $this->localStorage->uploadFile($tmpProcessedImageFile, true);

        return $this->createManipulatedPhotoEntity($photo->getCamera(), $processedImage);
    }

    /**
     * @param Photo $photo
     * @return Photo
     * @throws ImageManipulationException
     */
    public function rotateWithSettings(Photo $photo)
    {
        try {
            $file = $this->storageRetriever->getFileFromPhoto($photo);
        } catch (PhotoWithoutLinkedFileException $e) {
            throw new ImageManipulationException();
        }

        try {
            $fileObject = new FileObject($file->getFullPath());
        } catch (FileNotFoundException $e) {
            // TODO update photo entity with invalidity?
            throw new ImageManipulationException();
        }

        // TODO switch for different image types?
        $image = $this->imageProcessor->createFromPng($fileObject->getRealPath());
        $settings = $photo->getCamera()->getManipulationSettings();

        if (isset($settings->rotateAngle)) {
            switch ($photo->getCamera()->getSegment()->getType()) {
                case SegmentType::QUICK_SNACK;
                case SegmentType::READY_MEAL:
                    $image = $this->imageProcessor->imageRotate($image, (float) $settings->rotateAngle, 0);
                    break;
                case SegmentType::GRILL:
                    $image = $this->imageProcessor->imageRotateWithCrop($image, (float) $settings->rotateAngle, 0);
                    break;
            }

            if (!$image) {
                throw new ImageManipulationException();
            }
        }

        try {
            $tmpProcessedImageFile = $this->tmpImageFileHandler->saveTmpPngFromGd($image);
        } catch (ImageResourceException $e) {
            throw new ImageManipulationException();
        }
        $processedImage = $this->localStorage->uploadFile($tmpProcessedImageFile, true);

        return $this->createManipulatedPhotoEntity($photo->getCamera(), $processedImage);
    }

    /**
     * @param Camera $camera
     * @param File $file
     * @return Photo
     */
    private function createManipulatedPhotoEntity(Camera $camera, File $file): Photo
    {
        $processedPhoto = new Photo();
        $processedPhoto
            ->setCamera($camera)
            ->setStorageId($file->getId())
            ->setStorageType(FileStorageType::LOCAL)
            ->setIsAiProcessed(false)
            ->setIsValid(true)
            ->setIsManipulated(true)
        ;

        $this->entityManager->persist($processedPhoto);
        $this->entityManager->flush();

        return $processedPhoto;
    }
}
