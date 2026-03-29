<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Service;

use App\Entity\ProductGroup;
use App\Entity\System;
use App\Repository\ProductGroupRepository;
use DateTime;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;
use Symfony\Component\Validator\Validator\ValidatorInterface;

/**
 * Class UserService.
 */
class ProductGroupManager
{
    /**
     * @var ProductGroupRepository
     */
    private ProductGroupRepository $repository;

    private ValidatorInterface $validator;

    /**
     * ProductGroupManager constructor.
     *
     * @param ProductGroupRepository $repository
     */
    public function __construct(ProductGroupRepository $repository, ValidatorInterface $validator)
    {
        $this->repository = $repository;
        $this->validator = $validator;
    }

    /**
     * @param ProductGroup $productGroup
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function updateProductGroup(ProductGroup $productGroup): void
    {
        $this->repository->save($productGroup);
    }

    public function getProductGroup(int $id, System $system): ?ProductGroup
    {
        return $this->repository->findOneBy(['id' => $id, 'active' => true, 'system' => $system]);
    }

    /**
     * @param System $system
     *
     * @return ProductGroup[]
     */
    public function getProductGroups(System $system): array
    {
        return $this->repository->findBy(['active' => true, 'system' => $system]);
    }

    public function getNewProductGroup(System $system): ProductGroup
    {
        $productGroup = new ProductGroup();
        $productGroup->setActive(true);
        $productGroup->setSystem($system);
        $productGroup->setCreatedDate(new DateTime());
        $productGroup->setUpdatedDate(new DateTime());

        return $productGroup;
    }

    public function deleteProductGroup(ProductGroup $getProductGroup)
    {
    }
}
