<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Validation;

use App\Dto\ResponseDataDto;
use Symfony\Component\HttpFoundation\Response;

/**
 * Class UserResponseMapper.
 */
class UserResponseMapper
{
    private static array $httpCodeMapping = [
        ErrorCodes::INVALID_REQUEST => Response::HTTP_BAD_REQUEST,
        ErrorCodes::RESET_REQUEST_ALREADY_SENT => Response::HTTP_BAD_REQUEST,

        ErrorCodes::INVALID_RESET_TOKEN => Response::HTTP_UNAUTHORIZED,

        ErrorCodes::UNAUTHORIZED => Response::HTTP_FORBIDDEN,
        ErrorCodes::NO_SYSTEM_ASSIGNED_TO_USER => Response::HTTP_FORBIDDEN,
        ErrorCodes::SYSTEM_TERMINATED => Response::HTTP_FORBIDDEN,
        ErrorCodes::PASSWORD_CHANGE_REQUIRED => Response::HTTP_FORBIDDEN,
        ErrorCodes::USER_DISABLED => Response::HTTP_FORBIDDEN,

        ErrorCodes::BLOCKED_BY_TRAINING_IN_PROGRESS => Response::HTTP_CONFLICT,
        ErrorCodes::LINKED_BY_OTHER_RESOURCE => Response::HTTP_CONFLICT,
    ];

    public function mapErrorCode($errorCode): ResponseDataDto
    {
        if (!empty(self::$httpCodeMapping[$errorCode])) {
            return new ResponseDataDto(['code' => $errorCode], self::$httpCodeMapping[$errorCode]);
        }

        return null;
    }
}
