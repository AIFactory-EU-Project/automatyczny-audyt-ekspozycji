<?php

namespace App\Service;

use App\Exception\FileAccessException;
use App\Exception\ImageResourceException;
use Symfony\Component\Filesystem\Filesystem;
use Symfony\Component\HttpFoundation\File\File;

class TmpImageFileHandler
{
    private const TEMPORARY_FILE_LOCATION = '/tmp/';

    private const CAMERA_IMAGE_TYPE = 'png';

    /**
     * @var Filesystem
     */
    private $filesystem;

    public function __construct(Filesystem $filesystem)
    {
        $this->filesystem = $filesystem;
    }

    /**
     * @param string $file
     * @return File
     * @throws FileAccessException
     */
    public function saveTmpPngFromStream(string $file): File
    {
        $tmpName = $this->generateTmpPngName();
        $tmpFullPath = $this->generateTmpFileFullLocation($tmpName);
        $this->filesystem->touch($tmpFullPath);
        // TODO permission and directory error handling
        $fileStream = fopen($tmpFullPath, 'w+');
        if (!$fileStream) {
            throw new FileAccessException();
        }
        fwrite($fileStream, $file);
        fclose($fileStream);

        return new File($tmpFullPath);
    }

    /**
     * @param $image
     * @return File
     * @throws ImageResourceException
     */
    public function saveTmpPngFromGd($image): File
    {
        $tmpName = $this->generateTmpPngName();
        $tmpFullPath = $this->generateTmpFileFullLocation($tmpName);

        // TODO check if resource?
        $result = imagepng($image, $tmpFullPath);
        if (!$result) {
            throw new ImageResourceException();
        }
        imagedestroy($image);

        return new File($tmpFullPath);
    }

    /**
     * @return string
     */
    private function generateTmpPngName(): string
    {
        return uniqid('', true) . '.' . self::CAMERA_IMAGE_TYPE;
    }

    /**
     * @param $fileName
     * @return string
     */
    private function generateTmpFileFullLocation($fileName): string
    {
        return self::TEMPORARY_FILE_LOCATION . $fileName;
    }
}
