<?php

namespace App\Service;

use App\Utility\DBAL\Type\SegmentType;

class SegmentTranslator
{
    public function apiSegmentValidator(string $apiSegmentType): bool
    {
        $segmentType = $this->apiSegmentToDbSegment($apiSegmentType);
        return array_key_exists($segmentType, SegmentType::$choices);
    }

    public function apiSegmentToDbSegment(string $apiSegmentType): string
    {
        $ucApiSegmentType = strtoupper($apiSegmentType);
        return str_replace('-', '_', $ucApiSegmentType);
    }

    public function dbSegmentToApiSegment(string $segmentType): string
    {
        $lcSegmentType = strtolower($segmentType);
        return str_replace('_', '-', $lcSegmentType);
    }
}
