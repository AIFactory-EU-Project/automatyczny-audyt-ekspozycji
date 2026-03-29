<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Exception;

use Exception;

/**
 * Class UserAuthException.
 */
class UserAuthException extends Exception
{
    private string $errorCode;

    /**
     * UserAuthException constructor.
     *
     * @param $errorCode
     */
    public function __construct($errorCode)
    {
        parent::__construct();
        $this->errorCode = $errorCode;
    }

    /**
     * @return string
     */
    public function getErrorCode(): string
    {
        return $this->errorCode;
    }
}
