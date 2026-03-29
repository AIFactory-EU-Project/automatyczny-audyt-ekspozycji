<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Event\ProductGroupManagement;

use App\Entity\ProductGroup;
use App\Event\AbstractSystemActionEvent;

class DeleteProductGroupEvent extends AbstractSystemActionEvent
{
    private ?ProductGroup $productGroup = null;

    private int $id = 0;

    public function getId(): int
    {
        return $this->id;
    }

    public function setId(int $id): void
    {
        $this->id = $id;
    }

    public function getProductGroup(): ?ProductGroup
    {
        return $this->productGroup;
    }

    public function setProductGroup(?ProductGroup $productGroup): void
    {
        $this->productGroup = $productGroup;
    }
}
