<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Event\CategoryManagement;

use App\Entity\Category;
use App\Event\AbstractSystemActionEvent;

class UpdateCategoryEvent extends AbstractSystemActionEvent
{
    private ?Category $category = null;

    private int $id = 0;

    public function getId(): int
    {
        return $this->id;
    }

    public function setId(int $id): void
    {
        $this->id = $id;
    }

    public function getCategory(): ?Category
    {
        return $this->category;
    }

    public function setCategory(?Category $category): void
    {
        $this->category = $category;
    }
}
