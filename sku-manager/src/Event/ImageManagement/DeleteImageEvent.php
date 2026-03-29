<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Event\ImageManagement;

use App\Entity\Image;
use App\Event\AbstractSystemActionEvent;

class DeleteImageEvent extends AbstractSystemActionEvent
{
    private int $id = 0;

    private ?Image $image = null;

    public function getImage(): ?Image
    {
        return $this->image;
    }

    public function setImage(?Image $image): void
    {
        $this->image = $image;
    }

    /**
     * @return int
     */
    public function getId(): int
    {
        return $this->id;
    }

    /**
     * @param int $id
     */
    public function setId(int $id): void
    {
        $this->id = $id;
    }
}
