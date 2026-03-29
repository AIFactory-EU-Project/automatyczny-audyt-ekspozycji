<?php

namespace App\Service\Uploader;

use App\Entity\File;
use App\Utility\DBAL\Type\FileStorageType;
use Symfony\Component\HttpFoundation\File\File as FileObject;

class GoogleStorage implements FileUploader
{

    /**
     * @param FileObject $file
     * @return File
     */
    public function uploadFile(FileObject $file): File
    {
        // TODO: Implement uploadFile() method.
        return new File;
    }

    /**
     * @param File $file
     * @return bool
     */
    public function removeFile(File $file): bool
    {
        // TODO: Implement removeFile() method.
        return false;
    }

    public function getStorageType(): string
    {
        // TODO: Implement getStorageType() method.
        return FileStorageType::GOOGLE_CLOUD_STORAGE;
    }
}
