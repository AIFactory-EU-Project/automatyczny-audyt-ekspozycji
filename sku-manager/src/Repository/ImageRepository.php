<?php
/**
 * @license AiFactory
 */

namespace App\Repository;

use App\Entity\Image;
use App\Entity\System;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Common\Persistence\ManagerRegistry;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;

/**
 * @method Image|null find($id, $lockMode = null, $lockVersion = null)
 * @method Image|null findOneBy(array $criteria, array $orderBy = null)
 * @method Image[]    findAll()
 * @method Image[]    findBy(array $criteria, array $orderBy = null, $limit = null, $offset = null)
 */
class ImageRepository extends ServiceEntityRepository
{
    /**
     * ImageRepository constructor.
     *
     * @param ManagerRegistry $registry
     */
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, Image::class);
    }

    /**
     * @param Image $user
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function save(Image $user): void
    {
        $this->_em->persist($user);
        $this->_em->flush();
    }

    /**
     * @param System $system
     *
     * @return Image[]
     */
    public function findAllBySystem(System $system)
    {
        $images = $this->createQueryBuilder('i')
            ->join('i.product', 'p')
            ->andWhere('p.system = :system_id')
            ->andWhere('i.active = :status_active')
            ->setParameter('system_id', $system->getId())
            ->setParameter('status_active', 1)
            ->addOrderBy('i.id', 'asc')
            ->getQuery()
            ->getResult();

        return $images;
    }
}
