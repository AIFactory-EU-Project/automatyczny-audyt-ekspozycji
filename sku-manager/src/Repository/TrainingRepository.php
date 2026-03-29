<?php
/**
 * @license AiFactory
 */

namespace App\Repository;

use App\Entity\System;
use App\Entity\Training;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Common\Persistence\ManagerRegistry;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;

/**
 * @method Training|null find($id, $lockMode = null, $lockVersion = null)
 * @method Training|null findOneBy(array $criteria, array $orderBy = null)
 * @method Training[]    findAll()
 * @method Training[]    findBy(array $criteria, array $orderBy = null, $limit = null, $offset = null)
 */
class TrainingRepository extends ServiceEntityRepository
{
    /**
     * TrainingRepository constructor.
     *
     * @param ManagerRegistry $registry
     */
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, Training::class);
    }

    /**
     * @param Training $user
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function save(Training $user): void
    {
        $this->_em->persist($user);
        $this->_em->flush();
    }

    public function findAllBySystem(System $system)
    {
        $systems = $this->createQueryBuilder('t')
            ->join('t.productGroup', 'p')
            ->andWhere('p.system = :system_id')
            ->andWhere('t.active = :status_active')
            ->setParameter('system_id', $system->getId())
            ->setParameter('status_active', 1)
            ->addOrderBy('t.id', 'asc')
            ->getQuery()
            ->getResult();

        return $systems;
    }
}
