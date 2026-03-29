<?php

namespace App\Service;

use App\Entity\File;
use App\Entity\Photo;
use App\Exception\PhotoWithoutLinkedFileException;
use App\Utility\DBAL\Type\FileStorageType;
use Doctrine\ORM\EntityManagerInterface;

class StorageRetriever
{
    private EntityManagerInterface $em;

    public function __construct(
        EntityManagerInterface $entityManager
    ) {
        $this->em = $entityManager;
    }

    /**
     * @param Photo $photo
     * @return File
     * @throws PhotoWithoutLinkedFileException
     */
    public function getFileFromPhoto(Photo $photo): File
    {
        switch ($photo->getStorageType()) {
            case FileStorageType::LOCAL:
                $file = $this->getLocalFile($photo);
                break;
            // TODO implement google storage retrieval and possibly cache'ing?
        }

        return $file;
    }

    /**
     * @param Photo $photo
     * @return File
     * @throws PhotoWithoutLinkedFileException
     */
    private function getLocalFile(Photo $photo): File
    {
        $fileRepo = $this->em->getRepository(File::class);
        /** @var File $file */
        $file = $fileRepo->find((int)$photo->getStorageId());
        if (empty($file)) {
            throw new PhotoWithoutLinkedFileException();
        }

        return $file;
    }
}
