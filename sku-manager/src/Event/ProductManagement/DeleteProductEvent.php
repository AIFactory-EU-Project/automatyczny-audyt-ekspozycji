<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Event\ProductManagement;

use App\Entity\Product;
use App\Event\AbstractSystemActionEvent;

class DeleteProductEvent extends AbstractSystemActionEvent
{
    private ?Product $product = null;

    private int $id = 0;

    public function getId(): int
    {
        return $this->id;
    }

    public function setId(int $id): void
    {
        $this->id = $id;
    }

    public function getProduct(): ?Product
    {
        return $this->product;
    }

    public function setProduct(?Product $product): void
    {
        $this->product = $product;
    }
}
