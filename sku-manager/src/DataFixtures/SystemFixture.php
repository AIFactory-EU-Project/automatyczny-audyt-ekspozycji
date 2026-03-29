<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\DataFixtures;

use App\Entity\System;
use DateTime;
use Doctrine\Bundle\FixturesBundle\Fixture;
use Doctrine\Persistence\ObjectManager;
use Exception;

/**
 * Class SystemFixture.
 */
class SystemFixture extends Fixture
{
    /**
     * @param ObjectManager $manager
     *
     * @throws Exception
     */
    public function load(ObjectManager $manager)
    {
        $system = new System();
        $system->setCreatedDate(new DateTime());
        $system->setUpdatedDate(new DateTime());
        $system->setName('sample-system-human-code');
        $system->setRegion('sample-system-region');
        $system->setActive(true);
        $system->setContact('system.contact@placeholder.test');
        $manager->persist($system);
        $manager->flush();
    }
}
