<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Event\CategoryManagement;

use App\Entity\Category;
use App\Event\AbstractSystemActionEvent;

class UpdateCategoryValidEvent extends AbstractSystemActionEvent
{
    private ?Category $category = null;

    public function getCategory(): ?Category
    {
        return $this->category;
    }

    public function setCategory(?Category $category): void
    {
        $this->category = $category;
    }
}
