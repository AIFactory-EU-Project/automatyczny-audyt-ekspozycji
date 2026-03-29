<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Event\BrandManagement;

use App\Entity\Brand;
use App\Event\AbstractSystemActionEvent;

class DeleteBrandEvent extends AbstractSystemActionEvent
{
    private ?Brand $brand = null;

    private int $id = 0;

    public function getId(): int
    {
        return $this->id;
    }

    public function setId(int $id): void
    {
        $this->id = $id;
    }

    public function getBrand(): ?Brand
    {
        return $this->brand;
    }

    public function setBrand(?Brand $brand): void
    {
        $this->brand = $brand;
    }
}
