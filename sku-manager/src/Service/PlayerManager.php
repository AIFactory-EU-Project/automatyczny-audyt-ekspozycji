<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Service;

use App\Entity\Player;
use App\Entity\System;
use App\Repository\PlayerRepository;
use DateTime;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;
use Symfony\Component\Validator\Validator\ValidatorInterface;

/**
 * Class UserService.
 */
class PlayerManager
{
    /**
     * @var PlayerRepository
     */
    private PlayerRepository $repository;

    private ValidatorInterface $validator;

    public function __construct(PlayerRepository $repository, ValidatorInterface $validator)
    {
        $this->repository = $repository;
        $this->validator = $validator;
    }

    /**
     * @param Player $player
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function updatePlayer(Player $player): void
    {
        $player->setUpdatedDate(new DateTime());
        $this->repository->save($player);
    }

    public function getPlayer(int $id, System $system): ?Player
    {
        return $this->repository->findOneBy(['id' => $id, 'active' => true, 'system' => $system]);
    }

    public function validate(Player $player)
    {
        return $this->validator->validate($player);
    }

    /**
     * @param System $system
     *
     * @return Player[]
     */
    public function getPlayers(System $system): array
    {
        return $this->repository->findBy(['active' => true, 'system' => $system]);
    }

    public function getNewPlayer(System $system): Player
    {
        $player = new Player();
        $player->setActive(true);
        $player->setSystem($system);
        $player->setCreatedDate(new DateTime());
        $player->setUpdatedDate(new DateTime());

        return $player;
    }

    /**
     * @param Player $player
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function deletePlayer(Player $player)
    {
        $player->setActive(false);
        $this->updatePlayer($player);
    }
}
