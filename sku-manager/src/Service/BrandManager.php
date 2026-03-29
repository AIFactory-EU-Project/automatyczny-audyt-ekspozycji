<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Service;

use App\Entity\Brand;
use App\Entity\System;
use App\Repository\BrandRepository;
use DateTime;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;
use Symfony\Component\Validator\Validator\ValidatorInterface;

/**
 * Class UserService.
 */
class BrandManager
{
    /**
     * @var BrandRepository
     */
    private BrandRepository $repository;

    private ValidatorInterface $validator;

    public function __construct(BrandRepository $repository, ValidatorInterface $validator)
    {
        $this->repository = $repository;
        $this->validator = $validator;
    }

    /**
     * @param Brand $brand
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function updateBrand(Brand $brand): void
    {
        $brand->setUpdatedDate(new DateTime());
        $this->repository->save($brand);
    }

    public function getBrand(int $id, System $system): ?Brand
    {
        return $this->repository->findOneBy(['id' => $id, 'active' => true, 'system' => $system]);
    }

    /**
     * @param System $system
     *
     * @return Brand[]
     */
    public function getBrands(System $system): array
    {
        return $this->repository->findBy(['active' => true, 'system' => $system]);
    }

    public function getNewBrand(System $system): Brand
    {
        $brand = new Brand();
        $brand->setActive(true);
        $brand->setSystem($system);
        $brand->setCreatedDate(new DateTime());
        $brand->setUpdatedDate(new DateTime());

        return $brand;
    }

    /**
     * @param Brand $brand
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function deleteBrand(Brand $brand)
    {
        $brand->setActive(false);
        $this->updateBrand($brand);
    }
}
