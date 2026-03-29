<?php

namespace App\Service;

use PHPUnit\Framework\TestCase;
use Symfony\Component\Filesystem\Filesystem;
use Symfony\Component\HttpFoundation\File\File;

function uniqid()
{
    return 'thisisareallyuniqueid';
}

function fopen($filePath, $mode)
{
    return 'file-handle-replacement';
}

function fwrite($filePointer, $file)
{
    return;
}

function fclose($filePointer)
{
    return;
}

class TmpFileHandlerTest extends TestCase
{
    // TODO test bad paths
    public function testSaveTmpFileStreamReturnsFileObject()
    {
        $fileSystemComponent = new Filesystem();

        $fileStreamMock = 'thatwouldbeafileimagebutobviouslyitsnonsense';
        $tmpFileHandler = new TmpImageFileHandler($fileSystemComponent);
        $result = $tmpFileHandler->saveTmpPngFromStream($fileStreamMock);

        $fileObject = new File('/tmp/' . uniqid() . '.png');
        $this->assertEquals($result, $fileObject);
    }
}