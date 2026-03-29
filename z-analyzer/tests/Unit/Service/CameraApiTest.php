<?php

namespace App\Service;

use App\Entity\Camera;
use App\Entity\Photo;
use App\Entity\Shop;
use App\Provider\ApiClient;
use App\Service\Uploader\LocalStorage;
use App\Utility\DBAL\Type\FileStorageType;
use Doctrine\ORM\EntityManagerInterface;
use PHPUnit\Framework\TestCase;
use Symfony\Component\DependencyInjection\ParameterBag\ParameterBagInterface;
use Symfony\Component\HttpClient\MockHttpClient;
use Symfony\Component\HttpClient\Response\MockResponse;
use Symfony\Component\HttpFoundation\File\File;
use App\Entity\File as FileEntity;

class CameraApiTest extends TestCase
{
    // TODO test bad paths
    public function testGetPhotoReturnsPhotoEntity()
    {
        $mockApiClient = $this->createMock(ApiClient::class);
        $mockApiClient
            ->expects($this->any())
            ->method('request')
            ->with($this->anything())
            ->willReturn('apiContentString');
        $mockEntityManager = $this->createMock(EntityManagerInterface::class);
        $mockEntityManager
            ->expects($this->any())
            ->method('persist')
            ->with($this->anything());
        $mockEntityManager
            ->expects($this->any())
            ->method('flush');
        $mockParams = $this->createMock(ParameterBagInterface::class);
        $mockParams
            ->expects($this->any())
            ->method('get')
            ->with($this->stringContains('ecosystem'))
            ->willReturn([
                'camera_service' => [
                    'location' => 'fake_camera_service_location/',
                    'credentials' => [
                        'login' => 'service_login',
                        'password' => 'service_password',
                    ]
                ]
            ]);
        $mockFileObject = $this->createMock(File::class);
        $mockFileObject
            ->expects($this->any())
            ->method('getPath')
            ->willReturn('/srv/local_storage/abcdefg_123456.png');
        $mockFileObject
            ->expects($this->any())
            ->method('getBasename')
            ->willReturn('abcdefg_123456.png');
        $mockFileObject
            ->expects($this->any())
            ->method('getExtension')
            ->willReturn('png');
        $mockFileObject
            ->expects($this->any())
            ->method('move')
            ->with(
                $this->stringContains('/srv/local_storage'),
                $this->stringContains('abcdefg_123456.png')
            )
            ->willReturn($mockFileObject);
        $mockFileEntity = $this->createMock(FileEntity::class);
        $mockFileEntity
            ->expects($this->any())
            ->method('getId')
            ->willReturn(1);
        $mockFileStorage = $this->createMock(LocalStorage::class);
        $mockFileStorage
            ->expects($this->any())
            ->method('uploadFile')
            ->willReturn($mockFileEntity);
        $mockTmpFileHandler = $this->createMock(TmpImageFileHandler::class);
        $mockTmpFileHandler
            ->expects($this->any())
            ->method('saveTmpPngFromStream')
            ->willReturn($mockFileObject);

        $shopEntity = new Shop();
        $shopEntity
            ->setName('arbuzik')
            ->setCode('arb-do');

        $mockCameraEntity = $this->createMock(Camera::class);
        $mockCameraEntity
            ->expects($this->any())
            ->method('getIp')
            ->willReturn('192.168.0.1');
        $mockCameraEntity
            ->expects($this->any())
            ->method('getType')
            ->willReturn('dahua');
        $mockCameraEntity
            ->expects($this->any())
            ->method('getId')
            ->willReturn(1);
        $mockCameraEntity
            ->expects($this->any())
            ->method('getShop')
            ->willReturn($shopEntity);

        $cameraApi = new CameraApi(
            $mockApiClient,
            $mockEntityManager,
            $mockParams,
            $mockTmpFileHandler,
            $mockFileStorage
        );

        $result = $cameraApi->getPhoto($mockCameraEntity);

        $photoEntity = new Photo();
        $photoEntity
            ->setStorageType(FileStorageType::LOCAL)
            ->setIsValid(true)
            ->setIsManipulated(false)
            ->setIsAiProcessed(false)
            ->setCamera($mockCameraEntity)
            ->setStorageId(1)
            ->setTime($result->getTime());

        $this->assertEquals($result, $photoEntity);
    }
}
