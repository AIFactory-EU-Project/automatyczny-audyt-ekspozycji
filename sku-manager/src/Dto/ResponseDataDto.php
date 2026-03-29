<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Dto;

class ResponseDataDto
{
    private $content;

    private int $code;

    public function __construct($content, $code)
    {
        $this->content = $content;
        $this->code = $code;
    }

    /**
     * @return mixed
     */
    public function getContent()
    {
        return $this->content;
    }

    /**
     * @return int
     */
    public function getCode(): int
    {
        return $this->code;
    }
}
