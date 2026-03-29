<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Service;

use App\Entity\System;
use App\Repository\SystemRepository;
use DateTime;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;
use Exception;
use Symfony\Component\Validator\ConstraintViolationListInterface;
use Symfony\Component\Validator\Validator\ValidatorInterface;

/**
 * Class UserService.
 */
class SystemManager
{
    private SystemRepository $repository;

    private ValidatorInterface $validator;

    /**
     * SystemManager constructor.
     *
     * @param SystemRepository   $repository
     * @param ValidatorInterface $validator
     */
    public function __construct(SystemRepository $repository, ValidatorInterface $validator)
    {
        $this->repository = $repository;
        $this->validator = $validator;
    }

    /**
     * @param System $system
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function updateSystem(System $system): void
    {
        $this->repository->save($system);
    }

    /**
     * @return System
     */
    public function getNewSystem(): System
    {
        $system = new System();
        try {
            $system->setCreatedDate(new DateTime());
            $system->setUpdatedDate(new DateTime());
        } catch (Exception $e) {
        }

        return $system;
    }

    /**
     * @param $name
     *
     * @return System|null
     */
    public function getSystemByName($name): ?System
    {
        return $this->repository->findOneBy(['name' => $name]);
    }

    /**
     * @param System $system
     *
     * @return ConstraintViolationListInterface
     */
    public function validateSystem(System $system): ConstraintViolationListInterface
    {
        return $this->validator->validate($system);
    }

    /**
     * @param System $system
     *
     * @return bool
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function addSystem(System $system): void
    {
        $system->setUpdatedDate(new DateTime());
        $this->repository->save($system);
    }
}
