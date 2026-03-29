<?php

namespace App\Service\Uploader;

use App\Entity\File;
use App\Utility\DBAL\Type\FileStorageType;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Component\DependencyInjection\ParameterBag\ParameterBagInterface;
use Symfony\Component\Filesystem\Exception\IOException;
use Symfony\Component\Filesystem\Filesystem;
use Symfony\Component\HttpFoundation\File\Exception\FileNotFoundException;
use Symfony\Component\HttpFoundation\File\File as FileObject;

class LocalStorage implements FileUploader
{
    private EntityManagerInterface $entityManager;
    private ParameterBagInterface $params;
    private Filesystem $filesystem;

    public function __construct(
        EntityManagerInterface $entityManager,
        ParameterBagInterface $params,
        Filesystem $filesystem
    ) {
        $this->entityManager = $entityManager;
        $this->params = $params;
        $this->filesystem = $filesystem;
    }

    /**
     * Saves given file object on set storage
     *
     * @param FileObject $file
     * @param bool $isTemporary
     * @return File
     */
    public function uploadFile(FileObject $file, $isTemporary = false): File
    {
        $newFileName = $this->generateFileName($file);

        $storageLocation = $this->params->get('local_storage')['location'];

        $targetFileObject = $file->move($storageLocation, $newFileName);
        $this->filesystem->chown($targetFileObject->getRealPath(), 'www-data');
        $this->filesystem->chgrp($targetFileObject->getRealPath(), 'www-data');

        $fileEntity = new File();
        $fileEntity
            ->setDirectory('')
            ->setStorageLocation($storageLocation)
            ->setName($targetFileObject->getBasename())
            ->setExtension($targetFileObject->getExtension())
            ->setTemporary($isTemporary)
        ;

        $this->entityManager->persist($fileEntity);
        $this->entityManager->flush();

        return $fileEntity;
    }

    /**
     * Removes file from storage
     *
     * @param File $file
     * @return bool
     */
    public function removeFile(File $file): bool
    {
        try {
            $fileObject = new FileObject($file->getFullPath());
        } catch (FileNotFoundException $e) {
            return false;
        }

        try {
            $this->filesystem->remove($fileObject->getRealPath());
        } catch (IOException $e) {
            return false;
        }

        $this->entityManager->remove($file);
        $this->entityManager->flush();

        return true;
    }

    /**
     * @param FileObject $file
     * @return string
     */
    private function generateFileName(FileObject $file): string
    {
        return uniqid() . '_' . time() . '.' . $file->getExtension();
    }

    /**
     * @return string
     */
    public function getStorageType(): string
    {
        return FileStorageType::LOCAL;
    }
}
