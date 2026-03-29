<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Event\ImageManagement;

use App\Entity\Image;
use App\Event\AbstractSystemActionEvent;

class UpdateImageEvent extends AbstractSystemActionEvent
{
    private ?Image $image = null;

    private int $id = 0;

    public function getId(): int
    {
        return $this->id;
    }

    public function setId(int $id): void
    {
        $this->id = $id;
    }

    public function getImage(): ?Image
    {
        return $this->image;
    }

    public function setImage(?Image $image): void
    {
        $this->image = $image;
    }
}
