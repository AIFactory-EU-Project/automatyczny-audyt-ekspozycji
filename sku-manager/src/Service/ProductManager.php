<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Service;

use App\Entity\Product;
use App\Entity\System;
use App\Repository\ProductRepository;
use DateTime;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;
use Symfony\Component\Validator\Validator\ValidatorInterface;

/**
 * Class UserService.
 */
class ProductManager
{
    /**
     * @var ProductRepository
     */
    private ProductRepository $repository;

    private ValidatorInterface $validator;

    /**
     * ProductManager constructor.
     *
     * @param ProductRepository $repository
     */
    public function __construct(ProductRepository $repository, ValidatorInterface $validator)
    {
        $this->repository = $repository;
        $this->validator = $validator;
    }

    /**
     * @param Product $product
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function updateProduct(Product $product): void
    {
        $product->setUpdatedDate(new DateTime());
        $this->repository->save($product);
    }

    public function getProduct(int $id, System $system): ?Product
    {
        return $this->repository->findOneBy(['id' => $id, 'active' => true, 'system' => $system]);
    }

    public function validate(Product $product)
    {
        return $this->validator->validate($product);
    }

    /**
     * @param System $system
     *
     * @return Product[]
     */
    public function getProducts(System $system): array
    {
        return $this->repository->findBy(['active' => true, 'system' => $system]);
    }

    public function getNewProduct(System $system): Product
    {
        $product = new Product();
        $product->setActive(true);
        $product->setSystem($system);
        $product->setCreatedDate(new DateTime());
        $product->setUpdatedDate(new DateTime());

        return $product;
    }

    /**
     * @param Product $product
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function deleteProduct(Product $product)
    {
        $product->setActive(false);
        $this->updateProduct($product);
    }
}
