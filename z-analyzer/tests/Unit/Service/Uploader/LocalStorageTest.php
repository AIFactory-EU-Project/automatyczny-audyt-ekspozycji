<?php

namespace App\Service\Uploader;

use Doctrine\ORM\EntityManagerInterface;
use PHPUnit\Framework\TestCase;
use Symfony\Component\DependencyInjection\ParameterBag\ParameterBagInterface;
use Symfony\Component\Filesystem\Filesystem;
use Symfony\Component\HttpFoundation\File\File;

function uniqid()
{
    return 'thisisareallyuniqueid';
}

function time()
{
    return '123456';
}

class LocalStorageTest extends TestCase
{
    // TODO test bad paths
    public function testUploadFileReturnsFileEntity()
    {
        $mockEntityManager = $this->createMock(EntityManagerInterface::class);
        $mockEntityManager
            ->expects($this->any())
            ->method('persist')
            ->with($this->anything());
        $mockEntityManager
            ->expects($this->any())
            ->method('flush');
        $mockFileObject = $this->createMock(File::class);
        $mockFileObject
            ->expects($this->any())
            ->method('getPath')
            ->willReturn('/data/nfs/dev/local_storage/' . uniqid() . '_' . time() . '.png');
        $mockFileObject
            ->expects($this->any())
            ->method('getBasename')
            ->willReturn(uniqid() . '_' . time() . '.png');
        $mockFileObject
            ->expects($this->any())
            ->method('getExtension')
            ->willReturn('png');
        $mockFileObject
            ->expects($this->any())
            ->method('move')
            ->with(
                $this->stringContains('/data/nfs/dev/local_storage/'),
                $this->stringContains(uniqid() . '_' . time() . '.png')
            )
            ->willReturn($mockFileObject);
        $mockParams = $this->createMock(ParameterBagInterface::class);
        $mockParams
            ->expects($this->any())
            ->method('get')
            ->with($this->stringContains('local_storage'))
            ->willReturn([
                'location' => '/data/nfs/dev/local_storage/'
            ]);

        $localStorage = new LocalStorage(
            $mockEntityManager,
            $mockParams,
            new Filesystem()
        );
        $result = $localStorage->uploadFile($mockFileObject);

        $fileEntity = new \App\Entity\File();
        $fileEntity
            ->setName(uniqid() . '_' . time() . '.png')
            ->setExtension('png')
            ->setStorageLocation('/data/nfs/dev/local_storage/')
            ->setDirectory('');

        $this->assertEquals($result, $fileEntity);
    }

    // TODO test bad paths
    public function testRemoveFileWithoutException()
    {
        $mockEntityManager = $this->createMock(EntityManagerInterface::class);
        $mockEntityManager
            ->expects($this->any())
            ->method('persist')
            ->with($this->anything());
        $mockEntityManager
            ->expects($this->any())
            ->method('flush');
        $mockParams = $this->createMock(ParameterBagInterface::class);

        $filesystem = new Filesystem();

        $fileEntity = new \App\Entity\File();
        $fileEntity
            ->setName(uniqid() . '_' . time() . '.png')
            ->setExtension('png')
            ->setStorageLocation('/data/nfs/dev/local_storage/')
            ->setDirectory('');

        $localStorage = new LocalStorage(
            $mockEntityManager,
            $mockParams,
            $filesystem
        );

        $filesystem->touch('/data/nfs/dev/local_storage/' . uniqid() . '_' . time() . '.png');

        $localStorage->removeFile($fileEntity);

        $this->assertFileNotExists('/data/nfs/dev/local_storage/' . uniqid() . '_' . time() . '.png');
    }

    public function testRemoveFileReturnsFalseOnNotFoundFile()
    {
        $mockEntityManager = $this->createMock(EntityManagerInterface::class);
        $mockEntityManager
            ->expects($this->any())
            ->method('persist')
            ->with($this->anything());
        $mockEntityManager
            ->expects($this->any())
            ->method('flush');
        $mockParams = $this->createMock(ParameterBagInterface::class);

        $filesystem = new Filesystem();

        $fileEntity = new \App\Entity\File();
        $fileEntity
            ->setName(uniqid() . '_' . time() . '.png')
            ->setExtension('png')
            ->setStorageLocation('/data/nfs/dev/local_storage/')
            ->setDirectory('')
        ;

        $localStorage = new LocalStorage(
            $mockEntityManager,
            $mockParams,
            $filesystem
        );

        $result = $localStorage->removeFile($fileEntity);

        $this->assertFalse($result);
    }
}
