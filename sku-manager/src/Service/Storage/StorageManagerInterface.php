<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Service\Storage;

interface StorageManagerInterface
{
    public function uploadMediaFile($sourcePath, string $destinationPath);

    public function getMediaPublicUrl(string $destinationPath): string;

    public function getNNPublicUrl(string $destinationPath): string;
}
