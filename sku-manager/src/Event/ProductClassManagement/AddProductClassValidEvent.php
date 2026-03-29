<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Event\ProductClassManagement;

use App\Entity\ProductClass;
use App\Event\AbstractSystemActionEvent;

class AddProductClassValidEvent extends AbstractSystemActionEvent
{
    private ?ProductClass $productClass = null;

    public function getProductClass(): ?ProductClass
    {
        return $this->productClass;
    }

    public function setProductClass(?ProductClass $productClass): void
    {
        $this->productClass = $productClass;
    }
}
