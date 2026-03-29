<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Tests\Service;

use App\Service\ImageManager;
use Symfony\Bundle\FrameworkBundle\Test\KernelTestCase;

/**
 * Class UserService.
 */
class ImageManagerTest extends KernelTestCase
{
    public function setUp()
    {
        parent::setUp();
        self::bootKernel();
    }

    public function testServiceInit(): void
    {
        $imageManager = static::$kernel->getContainer()->get(ImageManager::class);
        $this->assertInstanceOf(ImageManager::class, $imageManager);
    }
}
