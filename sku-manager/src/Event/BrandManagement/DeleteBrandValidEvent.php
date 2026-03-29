<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Event\BrandManagement;

use App\Entity\Brand;
use App\Event\AbstractSystemActionEvent;

class DeleteBrandValidEvent extends AbstractSystemActionEvent
{
    private ?Brand $brand = null;

    public function getBrand(): ?Brand
    {
        return $this->brand;
    }

    public function setBrand(?Brand $brand): void
    {
        $this->brand = $brand;
    }
}
