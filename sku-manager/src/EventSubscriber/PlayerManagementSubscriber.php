<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\EventSubscriber;

use App\Dto\ResponseDataDto;
use App\Event\PlayerManagement\AddPlayerEvent;
use App\Event\PlayerManagement\AddPlayerValidEvent;
use App\Event\PlayerManagement\DeletePlayerEvent;
use App\Event\PlayerManagement\DeletePlayerValidEvent;
use App\Event\PlayerManagement\UpdatePlayerEvent;
use App\Event\PlayerManagement\UpdatePlayerValidEvent;
use App\Form\PlayerType;
use App\Service\PlayerManager;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;
use Psr\Log\LoggerInterface;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Symfony\Component\Form\FormFactoryInterface;
use Symfony\Component\HttpFoundation\Response;

class PlayerManagementSubscriber implements EventSubscriberInterface
{
    private LoggerInterface $logger;
    private PlayerManager $playerManager;
    private FormFactoryInterface $formFactory;

    public function __construct(
        LoggerInterface $appLogger,
        PlayerManager $playerManager,
        FormFactoryInterface $formFactory
    ) {
        $this->logger = $appLogger;
        $this->playerManager = $playerManager;
        $this->formFactory = $formFactory;
    }

    public static function getSubscribedEvents(): array
    {
        return [
            AddPlayerEvent::class => 'onAddPlayer',
            AddPlayerValidEvent::class => 'onAddPlayerValid',
            UpdatePlayerEvent::class => 'onUpdatePlayer',
            UpdatePlayerValidEvent::class => 'onUpdatePlayerValid',
            DeletePlayerEvent::class => 'onDeletePlayer',
            DeletePlayerValidEvent::class => 'onDeletePlayerValid',
        ];
    }

    public function onAddPlayer(AddPlayerEvent $event)
    {
        $player = $this->playerManager->getNewPlayer($event->getSystem());
        $event->setPlayer($player);
        $form = $this->formFactory->create(PlayerType::class, $player);
        $data = json_decode($event->getRequest()->getContent(), true);
        $form->submit($data);

        if (!$form->isValid()) {
            $response = new ResponseDataDto(
                $form->getErrors(true),
                Response::HTTP_BAD_REQUEST
            );
            $event->setResponseData($response);

            return;
        }
    }

    /**
     * @param AddPlayerValidEvent $event
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function onAddPlayerValid(AddPlayerValidEvent $event)
    {
        $this->playerManager->updatePlayer($event->getPlayer());
    }

    public function onDeletePlayer(DeletePlayerEvent $event)
    {
        $player = $this->playerManager->getPlayer($event->getId(), $event->getSystem());
        $event->setPlayer($player);
        if (!$player) {
            $response = new ResponseDataDto(
                ['message' => 'Player not found'],
                Response::HTTP_NOT_FOUND
            );
            $event->setResponseData($response);

            return;
        }
    }

    /**
     * @param DeletePlayerValidEvent $event
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function onDeletePlayerValid(DeletePlayerValidEvent $event)
    {
        $this->playerManager->deletePlayer($event->getPlayer());
    }

    public function onUpdatePlayer(UpdatePlayerEvent $event)
    {
        $player = $this->playerManager->getPlayer($event->getId(), $event->getSystem());
        $event->setPlayer($player);
        if (!$player) {
            $response = new ResponseDataDto(
                ['message' => 'Player not found'],
                Response::HTTP_NOT_FOUND
            );
            $event->setResponseData($response);

            return;
        }

        $form = $this->formFactory->create(PlayerType::class, $player);
        $data = json_decode($event->getRequest()->getContent(), true);
        $form->submit($data);

        if (!$form->isValid()) {
            $response = new ResponseDataDto(
                $form->getErrors(true),
                Response::HTTP_BAD_REQUEST
            );
            $event->setResponseData($response);

            return;
        }
    }

    /**
     * @param UpdatePlayerValidEvent $event
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function onUpdatePlayerValid(UpdatePlayerValidEvent $event)
    {
        $this->playerManager->updatePlayer($event->getPlayer());
    }
}
