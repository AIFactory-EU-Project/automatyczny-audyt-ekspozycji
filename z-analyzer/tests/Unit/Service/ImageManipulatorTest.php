<?php

namespace App\Service;

use App\Entity\Camera;
use App\Entity\Photo;
use App\Provider\ImageProcessorProvider;
use App\Repository\FileRepository;
use App\Service\Uploader\LocalStorage;
use App\Utility\DataObject\ImageManipulationSettings;
use App\Utility\DBAL\Type\FileStorageType;
use Doctrine\ORM\EntityManagerInterface;
use PHPUnit\Framework\TestCase;
use Symfony\Component\Filesystem\Filesystem;
use Symfony\Component\HttpFoundation\File\File;

class ImageManipulatorTest extends TestCase
{
    // TODO test bad paths
    public function testIsTransformingCreatingNewPhoto()
    {
        $uniqid = uniqid();
        $filesystem = new Filesystem();
        $filesystem->touch('/tmp/a_temporary_test_file_' . $uniqid);
        $mockOriginalImageFileEntity = $this->createMock(\App\Entity\File::class);
        $mockOriginalImageFileEntity
            ->expects($this->any())
            ->method('getFullPath')
            ->willReturn('/tmp/a_temporary_test_file_' . $uniqid);
        $mockEntityManager = $this->createMock(EntityManagerInterface::class);
        $mockEntityManager
            ->expects($this->any())
            ->method('persist')
            ->with($this->anything());
        $mockEntityManager
            ->expects($this->any())
            ->method('flush');
        $mockFileObject = $this->createMock(File::class);
        $mockTmpFileHandler = $this->createMock(TmpImageFileHandler::class);
        $mockTmpFileHandler
            ->expects($this->any())
            ->method('saveTmpPngFromGd')
            ->with($this->anything())
            ->willReturn($mockFileObject);
        $mockProcessedImageFileEntity = $this->createMock(\App\Entity\File::class);
        $mockProcessedImageFileEntity
            ->expects($this->any())
            ->method('getId')
            ->willReturn(2);
        $mockLocalStorage = $this->createMock(LocalStorage::class);
        $mockLocalStorage
            ->expects($this->any())
            ->method('uploadFile')
            ->with($this->anything())
            ->willReturn($mockProcessedImageFileEntity);
        $mockImageProcessorProvider = $this->createMock(ImageProcessorProvider::class);
        $image = 'someImage';
        $mockImageProcessorProvider
            ->expects($this->any())
            ->method('createFromPng')
            ->with($this->anything())
            ->willReturn($image);
        $mockImageProcessorProvider
            ->expects($this->any())
            ->method('imageRotate')
            ->with($this->anything())
            ->willReturn($image);
        $mockImageProcessorProvider
            ->expects($this->any())
            ->method('imageCrop')
            ->with($this->anything())
            ->willReturn($image);
        $manipulationSettings = new ImageManipulationSettings();
        $manipulationSettings->rotateAngle = 12.1;
        $manipulationSettings->cropHeight = 10;
        $manipulationSettings->cropWidth = 100;
        $manipulationSettings->cropY = 42;
        $manipulationSettings->cropX = 411;
        $mockCameraEntity = $this->createMock(Camera::class);
        $mockCameraEntity
            ->expects($this->any())
            ->method('getManipulationSettings')
            ->willReturn($manipulationSettings);
        $originalPhoto = new Photo();
        $originalPhoto
            ->setCamera($mockCameraEntity)
            ->setStorageId('1');

        $processedPhoto = new Photo();
        $processedPhoto
            ->setCamera($mockCameraEntity)
            ->setStorageId('2')
            ->setStorageType(FileStorageType::LOCAL)
            ->setIsAiProcessed(false)
            ->setIsValid(true)
            ->setIsManipulated(true)
        ;

        $mockStorageRetriever = $this->createMock(StorageRetriever::class);
        $mockStorageRetriever
            ->expects($this->any())
            ->method('getFileFromPhoto')
            ->willReturn($mockOriginalImageFileEntity);


        $imageManipulator = new ImageManipulator(
            $mockEntityManager,
            $mockTmpFileHandler,
            $mockLocalStorage,
            $mockImageProcessorProvider,
            $mockStorageRetriever
        );

        $result = $imageManipulator->transformPhoto($originalPhoto);
        // Not testing time capabilities
        $processedPhoto->setTime($result->getTime());

        $this->assertEquals($result, $processedPhoto);
    }
}
