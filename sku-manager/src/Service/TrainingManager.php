<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Service;

use App\Entity\System;
use App\Entity\Training;
use App\Repository\TrainingRepository;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;
use Symfony\Component\Validator\Validator\ValidatorInterface;

/**
 * Class UserService.
 */
class TrainingManager
{
    private TrainingRepository $repository;

    private ValidatorInterface $validator;

    /**
     * TrainingManager constructor.
     *
     * @param TrainingRepository $repository
     * @param ValidatorInterface $validator
     */
    public function __construct(TrainingRepository $repository, ValidatorInterface $validator)
    {
        $this->repository = $repository;
        $this->validator = $validator;
    }

    /**
     * @param Training $training
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function updateTraining(Training $training): void
    {
        $this->repository->save($training);
    }

    public function getTraining(int $id, System $system): ?Training
    {
        $training = $this->repository->findOneBy(['id' => $id, 'active' => true, 'system' => $system]);
        if ($training->getProductGroup() && $training->getProductGroup()->getSystem()->getId() === $system->getId()) {
            return $training;
        }

        return null;
    }

    /**
     * @param System $system
     *
     * @return Training[]
     */
    public function getTrainings(System $system)
    {
        return $this->repository->findAllBySystem($system);
    }

    public function getNewTraining(System $system): Training
    {
        $training = new Training();

        return $training;
    }
}
