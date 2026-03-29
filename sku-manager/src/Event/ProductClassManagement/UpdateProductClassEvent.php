<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Event\ProductClassManagement;

use App\Entity\ProductClass;
use App\Event\AbstractSystemActionEvent;

class UpdateProductClassEvent extends AbstractSystemActionEvent
{
    private ?ProductClass $productClass = null;

    private int $id = 0;

    public function getId(): int
    {
        return $this->id;
    }

    public function setId(int $id): void
    {
        $this->id = $id;
    }

    public function getProductClass(): ?ProductClass
    {
        return $this->productClass;
    }

    public function setProductClass(?ProductClass $productClass): void
    {
        $this->productClass = $productClass;
    }
}
