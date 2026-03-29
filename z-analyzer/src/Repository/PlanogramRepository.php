<?php

namespace App\Repository;

use App\Entity\Planogram;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;

/**
 * @method Planogram|null find($id, $lockMode = null, $lockVersion = null)
 * @method Planogram|null findOneBy(array $criteria, array $orderBy = null)
 * @method Planogram[]    findAll()
 * @method Planogram[]    findBy(array $criteria, array $orderBy = null, $limit = null, $offset = null)
 */
class PlanogramRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, Planogram::class);
    }
}
