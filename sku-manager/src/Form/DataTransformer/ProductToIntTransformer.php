<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Form\DataTransformer;

use App\Entity\Product;
use App\Repository\ProductRepository;
use Symfony\Component\Form\DataTransformerInterface;

class ProductToIntTransformer implements DataTransformerInterface
{
    private ProductRepository $repository;

    public function __construct(ProductRepository $repository)
    {
        $this->repository = $repository;
    }

    public function transform($value)
    {
        if (!$value instanceof Product) {
            return null;
        }

        return $value->getId();
    }

    public function reverseTransform($value)
    {
        return $this->repository->find((int) $value);
    }
}
