<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Validation;

/**
 * Class ErrorCodes.
 */
class ErrorCodes
{
    //400 GENERIC VALIDATION CODE
    public const INVALID_REQUEST = 'INVALID_REQUEST';
    public const RESET_REQUEST_ALREADY_SENT = 'RESET_REQUEST_ALREADY_SENT';

    //400 BUSINESS VALIDATION CODES:

    //401 RESPONSE HANDLED BY LEXIK JWT
    public const INVALID_RESET_TOKEN = 'INVALID_RESET_TOKEN';

    //403 CODES
    public const UNAUTHORIZED = 'UNAUTHORIZED';
    public const NO_SYSTEM_ASSIGNED_TO_USER = 'NO_SYSTEM_ASSIGNED_TO_USER';
    public const SYSTEM_TERMINATED = 'SYSTEM_TERMINATED';
    public const PASSWORD_CHANGE_REQUIRED = 'PASSWORD_CHANGE_REQUIRED';
    public const USER_DISABLED = 'USER_DISABLED';

    //404 - no custom codes

    //409 CONFLICT CODES
    public const BLOCKED_BY_TRAINING_IN_PROGRESS = 'BLOCKED_BY_TRAINING_IN_PROGRESS';
    public const LINKED_BY_OTHER_RESOURCE = 'LINKED_IN_OTHER_RESOURCE';

    public const INVALID_CODES = [
        self::INVALID_REQUEST,
    ];

    public const CONFLICT_CODES = [
        self::BLOCKED_BY_TRAINING_IN_PROGRESS,
        self::LINKED_BY_OTHER_RESOURCE,
    ];

    public const FORBIDDEN_CODES = [
        self::UNAUTHORIZED,
        self::PASSWORD_CHANGE_REQUIRED,
        self::SYSTEM_TERMINATED,
        self::NO_SYSTEM_ASSIGNED_TO_USER,
        self::USER_DISABLED,
    ];
}
