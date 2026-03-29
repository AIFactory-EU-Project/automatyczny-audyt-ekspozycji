<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Event\ProductGroupManagement;

use App\Entity\ProductGroup;
use App\Event\AbstractSystemActionEvent;

class DeleteProductGroupValidEvent extends AbstractSystemActionEvent
{
    private ?ProductGroup $productGroup = null;

    public function getProductGroup(): ?ProductGroup
    {
        return $this->productGroup;
    }

    public function setProductGroup(?ProductGroup $productGroup): void
    {
        $this->productGroup = $productGroup;
    }
}
