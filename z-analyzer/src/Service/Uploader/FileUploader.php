<?php

namespace App\Service\Uploader;

use App\Entity\File;
use Symfony\Component\HttpFoundation\File\File as FileObject;

interface FileUploader
{
    /**
     * @param FileObject $file
     * @return File
     */
    public function uploadFile(FileObject $file): File;

    /**
     * @param File $file
     * @return bool
     */
    public function removeFile(File $file): bool;

    /**
     * @return string
     */
    public function getStorageType(): string;
}
