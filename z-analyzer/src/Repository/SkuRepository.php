<?php

namespace App\Repository;

use App\Entity\Sku;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;

/**
 * @method Sku|null find($id, $lockMode = null, $lockVersion = null)
 * @method Sku|null findOneBy(array $criteria, array $orderBy = null)
 * @method Sku[]    findAll()
 * @method Sku[]    findBy(array $criteria, array $orderBy = null, $limit = null, $offset = null)
 */
class SkuRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, Sku::class);
    }

    public function getSkuListByIndex(array $indexArray): array
    {
        $qb = $this->createQueryBuilder('sku');
        $qb
            ->where('sku.index IN(:index_array)')
            ->setParameter('index_array', array_values($indexArray))
        ;

        return $qb->getQuery()->getResult();
    }
}
