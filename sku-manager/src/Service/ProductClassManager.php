<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Service;

use App\Entity\ProductClass;
use App\Entity\System;
use App\Repository\ProductClassRepository;
use DateTime;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;
use Symfony\Component\Validator\Validator\ValidatorInterface;

/**
 * Class UserService.
 */
class ProductClassManager
{
    /**
     * @var ProductClassRepository
     */
    private ProductClassRepository $repository;

    private ValidatorInterface $validator;

    /**
     * ProductClassManager constructor.
     *
     * @param ProductClassRepository $repository
     */
    public function __construct(ProductClassRepository $repository, ValidatorInterface $validator)
    {
        $this->repository = $repository;
        $this->validator = $validator;
    }

    /**
     * @param ProductClass $productClass
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function updateProductClass(ProductClass $productClass): void
    {
        $this->repository->save($productClass);
    }

    public function getProductClass(int $id, System $system)
    {
        return $this->repository->findOneBy(['id' => $id, 'active' => true, 'system' => $system]);
    }

    public function getProductClasses(System $system)
    {
        return $this->repository->findBy(['active' => true, 'system' => $system]);
    }

    public function getNewProductClass(System $system): ProductClass
    {
        $productClass = new ProductClass();
        $productClass->setActive(true);
        $productClass->setSystem($system);
        $productClass->setCreatedDate(new DateTime());
        $productClass->setUpdatedDate(new DateTime());

        return $productClass;
    }

    public function deleteProductClass(ProductClass $getProductClass)
    {
    }
}
