<?php

namespace App\Repository;

use App\Entity\FailedImportAttempt;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\Persistence\ManagerRegistry;

/**
 * @method FailedImportAttempt|null find($id, $lockMode = null, $lockVersion = null)
 * @method FailedImportAttempt|null findOneBy(array $criteria, array $orderBy = null)
 * @method FailedImportAttempt[]    findAll()
 * @method FailedImportAttempt[]    findBy(array $criteria, array $orderBy = null, $limit = null, $offset = null)
 */
class FailedImportAttemptRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, FailedImportAttempt::class);
    }

    /**
     * @return ArrayCollection
     */
    public function getAllNotRetried()
    {
        $queryBuilder = $this->createQueryBuilder('f');
        $queryBuilder
            ->where('f.retried = :false')
            ->setParameter(':false', false)
        ;

        $result = $queryBuilder->getQuery()->getResult();
        return new ArrayCollection($result);
    }
}
