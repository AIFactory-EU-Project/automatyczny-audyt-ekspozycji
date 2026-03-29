<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Form\DataTransformer;

use App\Entity\Brand;
use App\Repository\BrandRepository;
use Symfony\Component\Form\DataTransformerInterface;

class BrandToIntTransformer implements DataTransformerInterface
{
    private BrandRepository $repository;

    public function __construct(BrandRepository $repository)
    {
        $this->repository = $repository;
    }

    public function transform($value)
    {
        if (!$value instanceof Brand) {
            return null;
        }

        return $value->getId();
    }

    public function reverseTransform($value)
    {
        return $this->repository->find((int) $value);
    }
}
