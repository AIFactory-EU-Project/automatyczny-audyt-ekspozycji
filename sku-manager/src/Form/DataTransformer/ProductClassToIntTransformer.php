<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Form\DataTransformer;

use App\Entity\ProductClass;
use App\Repository\ProductClassRepository;
use Symfony\Component\Form\DataTransformerInterface;

class ProductClassToIntTransformer implements DataTransformerInterface
{
    private ProductClassRepository $repository;

    public function __construct(ProductClassRepository $repository)
    {
        $this->repository = $repository;
    }

    public function transform($value)
    {
        if (!$value instanceof ProductClass) {
            return null;
        }

        return $value->getId();
    }

    public function reverseTransform($value)
    {
        return $this->repository->find((int) $value);
    }
}
