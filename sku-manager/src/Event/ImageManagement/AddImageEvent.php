<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Event\ImageManagement;

use App\Entity\Image;
use App\Event\AbstractSystemActionEvent;

class AddImageEvent extends AbstractSystemActionEvent
{
    private ?Image $image = null;

    public function getImage(): ?Image
    {
        return $this->image;
    }

    public function setImage(?Image $image): void
    {
        $this->image = $image;
    }
}
