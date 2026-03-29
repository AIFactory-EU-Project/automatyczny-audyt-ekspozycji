<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Event\ProductManagement;

use App\Entity\Product;
use App\Event\AbstractSystemActionEvent;

class AddProductEvent extends AbstractSystemActionEvent
{
    private ?Product $product = null;

    public function getProduct(): ?Product
    {
        return $this->product;
    }

    public function setProduct(?Product $product): void
    {
        $this->product = $product;
    }
}
