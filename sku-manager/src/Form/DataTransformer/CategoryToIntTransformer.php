<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Form\DataTransformer;

use App\Entity\Category;
use App\Repository\CategoryRepository;
use Symfony\Component\Form\DataTransformerInterface;

class CategoryToIntTransformer implements DataTransformerInterface
{
    private CategoryRepository $repository;

    public function __construct(CategoryRepository $repository)
    {
        $this->repository = $repository;
    }

    public function transform($value)
    {
        if (!$value instanceof Category) {
            return null;
        }

        return $value->getId();
    }

    public function reverseTransform($value)
    {
        return $this->repository->find((int) $value);
    }
}
