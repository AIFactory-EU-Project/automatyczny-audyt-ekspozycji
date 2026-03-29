<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Service;

use App\Entity\Category;
use App\Entity\System;
use App\Repository\CategoryRepository;
use DateTime;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;
use Symfony\Component\Validator\Validator\ValidatorInterface;

/**
 * Class UserService.
 */
class CategoryManager
{
    /**
     * @var CategoryRepository
     */
    private CategoryRepository $repository;

    private ValidatorInterface $validator;

    public function __construct(CategoryRepository $repository, ValidatorInterface $validator)
    {
        $this->repository = $repository;
        $this->validator = $validator;
    }

    /**
     * @param Category $category
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function updateCategory(Category $category): void
    {
        $category->setUpdatedDate(new DateTime());
        $this->repository->save($category);
    }

    public function getCategory(int $id, System $system): ?Category
    {
        return $this->repository->findOneBy(['id' => $id, 'active' => true, 'system' => $system]);
    }

    /**
     * @param System $system
     *
     * @return Category[]
     */
    public function getCategorys(System $system): array
    {
        return $this->repository->findBy(['active' => true, 'system' => $system]);
    }

    public function getNewCategory(System $system): Category
    {
        $category = new Category();
        $category->setActive(true);
        $category->setSystem($system);
        $category->setCreatedDate(new DateTime());
        $category->setUpdatedDate(new DateTime());

        return $category;
    }

    /**
     * @param Category $category
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function deleteCategory(Category $category)
    {
        $category->setActive(false);
        $this->updateCategory($category);
    }
}
