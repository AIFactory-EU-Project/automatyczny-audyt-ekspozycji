<?php

namespace App\Utility\DBAL\Type;

use Fresh\DoctrineEnumBundle\DBAL\Types\AbstractEnumType;

class FileStorageType extends AbstractEnumType
{
    public const LOCAL = 'LOCAL';
    public const GOOGLE_CLOUD_STORAGE = 'GOOGLE_CLOUD_STORAGE';

    protected static $choices = [
        self::LOCAL => 'Local',
        self::GOOGLE_CLOUD_STORAGE => 'Google Cloud Storage',
    ];
}