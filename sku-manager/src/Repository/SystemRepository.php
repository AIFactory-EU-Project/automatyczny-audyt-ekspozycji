<?php
/**
 * @license AiFactory
 */

namespace App\Repository;

use App\Entity\System;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Common\Persistence\ManagerRegistry;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;

/**
 * @method System|null find($id, $lockMode = null, $lockVersion = null)
 * @method System|null findOneBy(array $criteria, array $orderBy = null)
 * @method System[]    findAll()
 * @method System[]    findBy(array $criteria, array $orderBy = null, $limit = null, $offset = null)
 */
class SystemRepository extends ServiceEntityRepository
{
    /**
     * SystemRepository constructor.
     *
     * @param ManagerRegistry $registry
     */
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, System::class);
    }

    /**
     * @param System $user
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function save(System $user): void
    {
        $this->_em->persist($user);
        $this->_em->flush();
    }
}
