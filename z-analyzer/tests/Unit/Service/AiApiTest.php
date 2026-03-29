<?php

namespace Unit\Service;

use App\Entity\Camera;
use App\Entity\File as FileEntity;
use App\Entity\Photo;
use App\Entity\Shop;
use App\Provider\ApiClient;
use App\Service\ApiConnection\AiApi;
use App\Service\StorageRetriever;
use App\Service\TmpImageFileHandler;
use App\Service\Uploader\LocalStorage;
use App\Utility\DBAL\Type\FileStorageType;
use Doctrine\ORM\EntityManagerInterface;
use PHPUnit\Framework\TestCase;
use Symfony\Component\DependencyInjection\ParameterBag\ParameterBagInterface;
use Symfony\Component\HttpFoundation\File\File;

class AiApiTest extends TestCase
{

    public function testRemoveFacesReturnsValidPhotoEntity()
    {
        $mockApiClient = $this->createMock(ApiClient::class);
        $mockApiClient
            ->expects($this->any())
            ->method('request')
            ->with($this->anything())
            ->willReturn(json_encode(['message' => 'string', 'status' => 'success']));
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
                'ai_service' => [
                    'location' => 'fake_ai_service_location/'
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

        $mockStorageRetriever = $this->createMock(StorageRetriever::class);
        $mockStorageRetriever
            ->expects($this->any())
            ->method('getFileFromPhoto')
            ->willReturn($mockFileEntity);

        $mockInputPhoto = $this->createMock(Photo::class);
        $mockInputPhoto
            ->expects($this->any())
            ->method('getCamera')
            ->willReturn($mockCameraEntity);

        $aiApi = new AiApi(
            $mockApiClient,
            $mockEntityManager,
            $mockParams,
            $mockTmpFileHandler,
            $mockFileStorage,
            $mockStorageRetriever
        );

        $result = $aiApi->removeFaces($mockInputPhoto);

        $photoEntity = new Photo();
        $photoEntity
            ->setStorageType(FileStorageType::LOCAL)
            ->setIsValid(true)
            ->setIsManipulated(true)
            ->setIsAiProcessed(false)
            ->setCamera($mockCameraEntity)
            ->setStorageId(1)
            ->setTime($result->getTime());

        $this->assertEquals($result, $photoEntity);
    }

    public function testVerifyReadyMealPhoto()
    {

    }

    public function testVerifyQuickSnackPhoto()
    {

    }

    public function testVerifyGrillPhoto()
    {

    }

//    public function testGetGrillReport()
//    {
//
//    }
//
//    public function testGetPlanogramReport()
//    {
//
//    }
}
