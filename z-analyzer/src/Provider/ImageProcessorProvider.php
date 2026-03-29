<?php

namespace App\Provider;

use App\Entity\Photo;
use App\Service\TmpImageFileHandler;
use App\Service\Uploader\LocalStorage;
use Exception;
use Symfony\Component\Process\Process;

class ImageProcessorProvider
{
    private TmpImageFileHandler $tmpImageFileHandler;
    private LocalStorage $localStorage;

    public function __construct(
        TmpImageFileHandler $tmpImageFileHandler,
        LocalStorage $localStorage
    ) {
        $this->tmpImageFileHandler = $tmpImageFileHandler;
        $this->localStorage = $localStorage;
    }

    /**
     * @param string $path
     * @return false|resource
     */
    public function createFromPng(string $path)
    {
        return imagecreatefrompng($path);
    }

    /**
     * @param $resource
     * @param float $rotateAngle
     * @param int $bgColor
     * @return false|resource
     */
    public function imageRotate($resource, float $rotateAngle, int $bgColor)
    {
        return imagerotate($resource, $rotateAngle, $bgColor);
    }

    /**
     * @param $resource
     * @param float $rotateAngle
     * @param int $bgColor
     * @return false|resource
     */
    public function imageRotateWithCrop($resource, float $rotateAngle, int $bgColor)
    {
        $imageWidth = imagesx($resource);
        $imageHeight = imagesy($resource);

        $rotatedImage = imagerotate($resource, $rotateAngle, $bgColor);
        $rotatedImageWidth = imagesx($rotatedImage);
        $rotatedImageHeight = imagesy($rotatedImage);

        return imagecrop($rotatedImage, [
            'width' => $imageWidth,
            'height' => $imageHeight,
            'x' => ($rotatedImageWidth / 2) - ($imageWidth / 2),
            'y' => ($rotatedImageHeight / 2) - ($imageHeight / 2)
        ]);
    }

    /**
     * @param $resource
     * @param array $paramsArray
     * @return bool|resource
     */
    public function imageCrop($resource, array $paramsArray)
    {
        return imagecrop($resource, $paramsArray);
    }

    /**
     * @param $resource
     * @param Photo $photo
     * @return false|resource
     * @throws Exception
     */
    public function adjustDepth($resource, Photo $photo)
    {
        $tmpFile = $this->tmpImageFileHandler->saveTmpPngFromGd($resource);
        $fileToTransform = $this->localStorage->uploadFile($tmpFile, true);

        $process = Process::fromShellCommandline(
            '$python $scriptLocation "$imageLocation" "$ipAddress" "$segment"'
        );

        $result = $process->run(null, [
            'python' => '/usr/bin/python3',
            'scriptLocation' => '/usr/src/app/bin/perspective_transformation.py',
            'imageLocation' => $fileToTransform->getFullPath(),
            'ipAddress' => $photo->getCamera()->getIp(),
            'segment' => strtolower($photo->getCamera()->getSegment()->getType()),
        ]);

        if ($result != 0) {
            throw new Exception(
                'Problem with Python transformative script \n' .
                $result .
                ' ' .
                $process->getErrorOutput()
            );
        }

        return $this->createFromPng($fileToTransform->getFullPath());
    }
}
