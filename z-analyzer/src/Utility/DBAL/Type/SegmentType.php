<?php

namespace App\Utility\DBAL\Type;

use Fresh\DoctrineEnumBundle\DBAL\Types\AbstractEnumType;

class SegmentType extends AbstractEnumType
{
    public const READY_MEAL = 'READY_MEAL';
    public const QUICK_SNACK = 'QUICK_SNACK';
    public const GRILL = 'GRILL';

    public static $choices = [
        self::READY_MEAL => 'Ready meal',
        self::QUICK_SNACK => 'Quick snack',
        self::GRILL => 'Grill',
    ];

    public static $shortChoices = [
        self::READY_MEAL => 'DG',
        self::QUICK_SNACK => 'SP',
        self::GRILL => 'RO',
    ];
}